---
name: frontend-architecture
description: |
  Frontend development guidelines. Read when:
  (1) Writing React/TypeScript code
  (2) Designing component structure
  (3) Managing state
---

# Frontend Architecture

## Standard Structure

```
src/
├── components/          # Reusable (ui/, features/)
├── pages/               # Page components
├── hooks/               # Custom hooks
├── services/            # API services
├── stores/              # State management
├── utils/               # Utilities
└── types/               # TypeScript types
```

## Design Patterns

**Component Composition**:
```tsx
const Avatar = ({ src, alt }) => <img src={src} alt={alt} className="avatar" />;
const UserCard = ({ user }) => (
  <div className="user-card">
    <Avatar src={user.avatar} alt={user.name} />
    <span>{user.name}</span>
  </div>
);
```

**Custom Hooks**:
```tsx
function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    fetchUser(userId).then(setUser).finally(() => setLoading(false));
  }, [userId]);
  return { user, loading };
}
```

**Type Safety**:
```tsx
interface User { id: string; name: string; email: string; }
interface UserCardProps { user: User; onClick?: (user: User) => void; }
```

## State Management

**Local**: `useState` for component-specific state
**Shared**: Zustand for global state
```tsx
const useStore = create((set) => ({
  user: null,
  setUser: (user) => set({ user }),
}));
```

## Styling

Tailwind CSS preferred:
```tsx
<button className="px-4 py-2 bg-blue-500 text-white rounded">Submit</button>
```
