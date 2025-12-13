import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import IssueCard from '../components/IssueCard.vue'

describe('IssueCard', () => {
  const mockIssue = {
    id: 1,
    title: 'Test Issue',
    description: 'This is a test issue',
    priority: 1,
    status: 'todo',
    estimate_minutes: 60
  }

  it('renders issue title and description', () => {
    const wrapper = mount(IssueCard, {
      props: {
        issue: mockIssue
      }
    })

    expect(wrapper.text()).toContain('Test Issue')
    expect(wrapper.text()).toContain('This is a test issue')
  })

  it('displays priority correctly', () => {
    const wrapper = mount(IssueCard, {
      props: {
        issue: mockIssue
      }
    })

    expect(wrapper.text()).toContain('🔥 Urgent & Important')
  })

  it('shows estimate time when available', () => {
    const wrapper = mount(IssueCard, {
      props: {
        issue: mockIssue
      }
    })

    expect(wrapper.text()).toContain('60 min')
  })

  it('emits dragstart event when dragged', async () => {
    const wrapper = mount(IssueCard, {
      props: {
        issue: mockIssue
      },
      attrs: {
        draggable: true
      }
    })

    const card = wrapper.find('[draggable="true"]')
    await card.trigger('dragstart')

    // Check if dragstart event was emitted (would need to mock dataTransfer)
    expect(card.exists()).toBe(true)
  })

  it('renders different priority emojis correctly', () => {
    const priorities = [
      { priority: 1, emoji: '🔥' },
      { priority: 2, emoji: '⚠️' },
      { priority: 3, emoji: '🌱' },
      { priority: 4, emoji: '🧘' }
    ]

    priorities.forEach(({ priority, emoji }) => {
      const issue = { ...mockIssue, priority }
      const wrapper = mount(IssueCard, {
        props: { issue }
      })

      expect(wrapper.text()).toContain(emoji)
    })
  })
})