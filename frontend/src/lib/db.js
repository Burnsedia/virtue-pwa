import { openDB } from 'idb';

const DB_NAME = 'virtue-pwa-db';
const DB_VERSION = 1;

const dbPromise = openDB(DB_NAME, DB_VERSION, {
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

export const db = {
  async get(storeName, key) {
    return (await dbPromise).get(storeName, key);
  },
  async getAll(storeName) {
    return (await dbPromise).getAll(storeName);
  },
  async set(storeName, value) {
    return (await dbPromise).put(storeName, value);
  },
  async setAll(storeName, values) {
    const tx = (await dbPromise).transaction(storeName, 'readwrite');
    for (const value of values) {
      tx.store.put(value);
    }
    await tx.done;
  },
  async delete(storeName, key) {
    return (await dbPromise).delete(storeName, key);
  },
  async clear(storeName) {
    return (await dbPromise).clear(storeName);
  },
};
