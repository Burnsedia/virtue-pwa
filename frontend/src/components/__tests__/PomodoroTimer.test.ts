import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import PomodoroTimer from '../PomodoroTimer.vue'

// Mock Audio with a constructable class so `new Audio()` in playSound() works
// (a vi.fn() with an arrow mockImplementation cannot be used with `new`).
class FakeAudio {
  play = vi.fn()
}
;(global as any).Audio = FakeAudio

describe('PomodoroTimer', () => {
  let wrapper: any

  beforeEach(() => {
    // Mock localStorage (jsdom's real in-memory Storage; see setup.ts)
    vi.spyOn(Storage.prototype, 'getItem').mockReturnValue(null)
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {})

    // Mock fetch for projects and issues. Resolve to empty by default so the
    // component's async fetchProjects()/fetchIssues() (called on mount) never
    // rejects with "Cannot read property 'json' of undefined".
    global.fetch = vi.fn().mockResolvedValue({ json: async () => [] })

    wrapper = mount(PomodoroTimer)
  })

  it('renders timer display', () => {
    expect(wrapper.text()).toContain('25:00') // Default work session
  })

  it('displays session buttons', () => {
    expect(wrapper.text()).toContain('Pomodoro')
    expect(wrapper.text()).toContain('Short Break')
    expect(wrapper.text()).toContain('Long Break')
  })

  it('has start, pause, and reset buttons', () => {
    const buttons = wrapper.findAll('button')
    expect(buttons.some((btn: any) => btn.text() === 'Start')).toBe(true)
    expect(buttons.some((btn: any) => btn.text() === 'Pause')).toBe(true)
    expect(buttons.some((btn: any) => btn.text() === 'Reset')).toBe(true)
  })

  it('requires issue selection to start work session', async () => {
    // Mock alert
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})

    // Try to start without selecting issue
    await wrapper.find('button').trigger('click')

    expect(alertSpy).toHaveBeenCalledWith('Please select an issue to work on.')
    alertSpy.mockRestore()
  })

  it('loads pomodoro settings from localStorage', () => {
    const mockSettings = {
      work: 30,
      shortBreak: 10,
      longBreak: 20
    }

    vi.spyOn(Storage.prototype, 'getItem').mockReturnValue(JSON.stringify(mockSettings))

    const newWrapper = mount(PomodoroTimer)
    expect(newWrapper.vm.pomodoroSettings).toEqual(mockSettings)
  })

  it('switches to long break after the 4th work session', async () => {
    // Mock issue selection
    await wrapper.setData({
      selectedIssue: 1,
      pomodoros: 3 // One less than 4
    })

    // Mock fetch for timelog creation
    global.fetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve({ id: 1 })
    })

    // Start timer. Enable fake timers first: the async startTimer creates its
    // setInterval only after awaiting fetch, so without this a real interval would
    // be created before fake timers take effect (and advanceTimersByTime ignores it).
    vi.useFakeTimers()
    const startButton = wrapper.findAll('button').find((btn: any) => btn.text() === 'Start')
    await startButton.trigger('click')

    // Simulate timer completion. Advancing 25 minutes lands `time` on 0, but the
    // else branch (completion) only fires on the next tick, so add one interval.
    vi.advanceTimersByTime(25 * 60 * 1000 + 1000) // 25 minutes + 1 tick

    // The 4th pomodoro completes -> long break (standard pomodoro cadence)
    expect(wrapper.vm.sessionType).toBe('longBreak')
    expect(wrapper.vm.pomodoros).toBe(4)

    vi.useRealTimers()
  })

  it('switches to long break after completing work session', async () => {
    await wrapper.setData({
      selectedIssue: 1,
      sessionType: 'shortBreak',
      // setData does not re-run resetTimer(), so set the timer to the
      // shortBreak duration (5 min) to match a real session switch.
      time: 5 * 60
    })

    // Mock fetch
    global.fetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve({ id: 1 })
    })

    // Start timer (fake timers first; see test above)
    vi.useFakeTimers()
    const startButton = wrapper.findAll('button').find((btn: any) => btn.text() === 'Start')
    await startButton.trigger('click')

    // Simulate timer completion. 5 minutes lands `time` on 0; add one tick for the
    // completion branch that then switches back to a work session.
    vi.advanceTimersByTime(5 * 60 * 1000 + 1000) // 5 minutes + 1 tick

    // Should switch back to work
    expect(wrapper.vm.sessionType).toBe('work')

    vi.useRealTimers()
  })

  it('plays sound when timer completes', async () => {
    const playSpy = vi.fn()

    // Real constructor so `new Audio(...)` in playSound() works.
    ;(global as any).Audio = class {
      play = playSpy
    }

    await wrapper.setData({
      selectedIssue: 1,
      time: 1 // 1 second remaining
    })

    // Mock fetch
    global.fetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve({ id: 1 })
    })

    // Start timer (fake timers first; see test above)
    vi.useFakeTimers()
    const startButton = wrapper.findAll('button').find((btn: any) => btn.text() === 'Start')
    await startButton.trigger('click')

    // Simulate timer completion. The interval fires once per second and decrements
    // `time` first; with time=1 the first tick reaches 0, so advance 2000ms to fire
    // a second tick that enters the else branch and calls playSound().
    vi.advanceTimersByTime(2000) // 2 seconds

    expect(playSpy).toHaveBeenCalled()

    vi.useRealTimers()
  })
})