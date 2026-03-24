# Frontend Architecture

<!--
  🎨 FRONTEND ARCHITECTURE
  
  Guidelines for frontend development within AHES.
-->

---

## 🎯 Overview

Frontend follows a component-based architecture with strong typing and test coverage.

---

## 📐 Standard Structure

```
src/
├── components/          # Reusable components
│   ├── ui/              # Design system
│   └── features/        # Feature components
├── pages/               # Page components
├── hooks/               # Custom hooks
├── services/            # API services
├── stores/              # State management
├── utils/               # Utilities
└── types/               # TypeScript types
```

---

## 🔧 Design Patterns

### 1. Component Composition

```tsx
// Small, focused components
const Avatar = ({ src, alt }) => (
  <img src={src} alt={alt} className="avatar" />
);

const UserCard = ({ user }) => (
  <div className="user-card">
    <Avatar src={user.avatar} alt={user.name} />
    <span>{user.name}</span>
  </div>
);
```

### 2. Custom Hooks

```tsx
// Extract reusable logic
function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchUser(userId).then(setUser).finally(() => setLoading(false));
  }, [userId]);
  
  return { user, loading };
}
```

### 3. Type Safety

```tsx
// Define clear interfaces
interface User {
  id: string;
  name: string;
  email: string;
}

interface UserCardProps {
  user: User;
  onClick?: (user: User) => void;
}
```

---

## 🔌 State Management

### Local State

```tsx
// Use for component-specific state
const [isOpen, setIsOpen] = useState(false);
```

### Shared State

```tsx
// Use Zustand for shared state
const useStore = create((set) => ({
  user: null,
  setUser: (user) => set({ user }),
}));
```

---

## 🎨 Styling

### Component Styles

```tsx
// Tailwind CSS preferred
<button className="px-4 py-2 bg-blue-500 text-white rounded">
  Submit
</button>
```

---

## 🔗 Related

- `ai/rules/coding.md` — Frontend coding standards
