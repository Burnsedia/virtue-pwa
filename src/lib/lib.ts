// lib/lib.ts
const GITHUB_API = 'https://api.github.com';

// Get from environment or inject
const GITHUB_TOKEN = import.meta.env.GITHUB_TOKEN || ''; // if SSR/backend
const DEFAULT_HEADERS = {
  Accept: 'application/vnd.github+json',
  Authorization: `Bearer ${GITHUB_TOKEN}`,
  'X-GitHub-Api-Version': '2022-11-28'
};

// 🧠 Fetch authenticated user
export async function getGitHubUser() {
  const res = await fetch(`${GITHUB_API}/user`, {
    headers: DEFAULT_HEADERS
  });

  if (!res.ok) throw new Error('Failed to fetch GitHub user');

  return await res.json();
}

// 🧠 Fetch issues from a repo
export async function getRepoIssues(owner: string, repo: string) {
  const res = await fetch(`${GITHUB_API}/repos/${owner}/${repo}/issues`, {
    headers: DEFAULT_HEADERS
  });

  if (!res.ok) throw new Error(`Failed to fetch issues for ${owner}/${repo}`);

  return await res.json();
}

// 🧠 Create issue
export async function createIssue(owner: string, repo: string, title: string, body = '') {
  const res = await fetch(`${GITHUB_API}/repos/${owner}/${repo}/issues`, {
    method: 'POST',
    headers: {
      ...DEFAULT_HEADERS,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ title, body })
  });

  if (!res.ok) throw new Error(`Failed to create issue: ${await res.text()}`);

  return await res.json();
}

