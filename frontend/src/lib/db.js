import { openDB } from 'idb';

const DB_NAME = 'virtue-pwa-db';
const DB_VERSION = 1;

let dbPromise;

function getDbPromise() {
  if (!dbPromise) {
    dbPromise = openDB(DB_NAME, DB_VERSION, {
      upgrade(db) {
        if (!db.objectStoreNames.contains('projects')) {
          db.createObjectStore('projects', { keyPath: 'id' });
        }
        if (!db.objectStoreNames.contains('issues')) {
          db.createObjectStore('issues', { keyPath: 'id' });
        }
        if (!db.objectStoreNames.contains('clients')) {
          db.createObjectStore('clients', { keyPath: 'id' });
        }
        if (!db.objectStoreNames.contains('invoices')) {
          db.createObjectStore('invoices', { keyPath: 'id' });
        }
      },
    });
  }
  return dbPromise;
}

export const db = {
  async get(storeName, key) {
    if (typeof window === 'undefined') return;
    return (await getDbPromise()).get(storeName, key);
  },
  async getAll(storeName) {
    if (typeof window === 'undefined') return;
    return (await getDbPromise()).getAll(storeName);
  },
  async set(storeName, value) {
    if (typeof window === 'undefined') return;
    return (await getDbPromise()).put(storeName, value);
  },
  async setAll(storeName, values) {
    if (typeof window === 'undefined') return;
    const tx = (await getDbPromise()).transaction(storeName, 'readwrite');
    for (const value of values) {
      tx.store.put(value);
    }
    await tx.done;
  },
  async delete(storeName, key) {
    if (typeof window === 'undefined') return;
    return (await getDbPromise()).delete(storeName, key);
  },
  async clear(storeName) {
    if (typeof window === 'undefined') return;
    return (await getDbPromise()).clear(storeName);
  },
};
