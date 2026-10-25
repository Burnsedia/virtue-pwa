import { vi } from 'vitest'

// Mock fetch globally
global.fetch = vi.fn()

// In-memory `localStorage` implementation.
//
// jsdom does not expose a real `Storage` here (`new Storage()` throws "Illegal
// constructor"), so we back `Storage.prototype` with a Map and hand out an
// instance via `Object.create(Storage.prototype)`. This matters because the
// PomodoroTimer tests spy on `Storage.prototype.getItem` -- the instance must
// inherit from the prototype for those spies to take effect. Missing keys
// return `null` (not `undefined`), so components doing
// `JSON.parse(localStorage.getItem(...))` no longer crash in mount().
const __memStore = new Map<string, string>()
const __storageProto: Storage = Storage.prototype

__storageProto.getItem = function (key) {
  return __memStore.has(key) ? (__memStore.get(key) ?? null) : null
}
__storageProto.setItem = function (key, value) {
  __memStore.set(key, String(value))
}
__storageProto.removeItem = function (key) {
  __memStore.delete(key)
}
__storageProto.clear = function () {
  __memStore.clear()
}

global.localStorage = Object.create(__storageProto) as Storage

// Mock matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(), // deprecated
    removeListener: vi.fn(), // deprecated
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})
