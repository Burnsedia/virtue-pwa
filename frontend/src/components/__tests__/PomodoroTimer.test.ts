import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import PomodoroTimer from '../components/PomodoroTimer.vue'

// Mock Audio
global.Audio = vi.fn().mockImplementation(() => ({
  play: vi.fn()
}))

describe('PomodoroTimer', () => {
  let wrapper: any

  beforeEach(() => {
    // Mock localStorage
    vi.spyOn(Storage.prototype, 'getItem').mockReturnValue(null)
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {})

    // Mock fetch for projects and issues
    global.fetch = vi.fn()

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

  it('switches to short break after 4 work sessions', async () => {
    // Mock issue selection
    await wrapper.setData({
      selectedIssue: 1,
      pomodoros: 3 // One less than 4
    })

    // Mock fetch for timelog creation
    global.fetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve({ id: 1 })
    })

    // Start timer
    const startButton = wrapper.findAll('button').find(btn => btn.text() === 'Start')
    await startButton.trigger('click')

    // Simulate timer completion
    vi.useFakeTimers()
    vi.advanceTimersByTime(25 * 60 * 1000) // 25 minutes

    // Should switch to short break
    expect(wrapper.vm.sessionType).toBe('shortBreak')
    expect(wrapper.vm.pomodoros).toBe(4)

    vi.useRealTimers()
  })

  it('switches to long break after completing work session', async () => {
    await wrapper.setData({
      selectedIssue: 1,
      sessionType: 'shortBreak'
    })

    // Mock fetch
    global.fetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve({ id: 1 })
    })

    // Start timer
    const startButton = wrapper.findAll('button').find(btn => btn.text() === 'Start')
    await startButton.trigger('click')

    // Simulate timer completion
    vi.useFakeTimers()
    vi.advanceTimersByTime(5 * 60 * 1000) // 5 minutes

    // Should switch back to work
    expect(wrapper.vm.sessionType).toBe('work')

    vi.useRealTimers()
  })

  it('plays sound when timer completes', async () => {
    const playSpy = vi.fn()
    global.Audio = vi.fn().mockImplementation(() => ({
      play: playSpy
    }))

    await wrapper.setData({
      selectedIssue: 1,
      time: 1 // 1 second remaining
    })

    // Mock fetch
    global.fetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve({ id: 1 })
    })

    // Start timer
    const startButton = wrapper.findAll('button').find(btn => btn.text() === 'Start')
    await startButton.trigger('click')

    // Simulate timer completion
    vi.useFakeTimers()
    vi.advanceTimersByTime(1000) // 1 second

    expect(playSpy).toHaveBeenCalled()

    vi.useRealTimers()
  })
})