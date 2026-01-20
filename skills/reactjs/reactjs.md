# React.js

## Composants

### Composant fonctionnel
```jsx
function Welcome({ name }) {
    return <h1>Bonjour, {name}</h1>;
}

// Arrow function
const Welcome = ({ name }) => {
    return <h1>Bonjour, {name}</h1>;
};

// Utilisation
<Welcome name="Alice" />
```

### Props
```jsx
function UserCard({ user, onEdit, children }) {
    return (
        <div className="card">
            <h2>{user.name}</h2>
            <p>{user.email}</p>
            <button onClick={() => onEdit(user.id)}>Modifier</button>
            {children}
        </div>
    );
}

// Props par défaut
function Button({ variant = 'primary', children }) {
    return <button className={variant}>{children}</button>;
}
```

## Hooks

### useState
```jsx
import { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);

    return (
        <div>
            <p>Compteur: {count}</p>
            <button onClick={() => setCount(count + 1)}>+1</button>
            <button onClick={() => setCount(prev => prev - 1)}>-1</button>
        </div>
    );
}

// État objet
const [user, setUser] = useState({ name: '', email: '' });
setUser(prev => ({ ...prev, name: 'John' }));
```

### useEffect
```jsx
import { useEffect, useState } from 'react';

function UserProfile({ userId }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Exécuté au montage et quand userId change
        const fetchUser = async () => {
            setLoading(true);
            const response = await fetch(`/api/users/${userId}`);
            const data = await response.json();
            setUser(data);
            setLoading(false);
        };
        fetchUser();

        // Cleanup (optionnel)
        return () => {
            // Annuler la requête si le composant est démonté
        };
    }, [userId]); // Dépendances

    if (loading) return <p>Chargement...</p>;
    return <div>{user?.name}</div>;
}
```

### useContext
```jsx
import { createContext, useContext, useState } from 'react';

const ThemeContext = createContext();

function ThemeProvider({ children }) {
    const [theme, setTheme] = useState('light');

    return (
        <ThemeContext.Provider value={{ theme, setTheme }}>
            {children}
        </ThemeContext.Provider>
    );
}

function ThemedButton() {
    const { theme, setTheme } = useContext(ThemeContext);

    return (
        <button
            className={theme}
            onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
        >
            Toggle Theme
        </button>
    );
}
```

### useRef
```jsx
import { useRef, useEffect } from 'react';

function TextInput() {
    const inputRef = useRef(null);

    useEffect(() => {
        inputRef.current.focus();
    }, []);

    return <input ref={inputRef} type="text" />;
}

// Valeur persistante sans re-render
function Timer() {
    const intervalRef = useRef(null);

    const start = () => {
        intervalRef.current = setInterval(() => {
            console.log('tick');
        }, 1000);
    };

    const stop = () => {
        clearInterval(intervalRef.current);
    };

    return (
        <>
            <button onClick={start}>Start</button>
            <button onClick={stop}>Stop</button>
        </>
    );
}
```

### useMemo et useCallback
```jsx
import { useMemo, useCallback } from 'react';

function ExpensiveComponent({ items, filter }) {
    // Mémorise le résultat du calcul
    const filteredItems = useMemo(() => {
        return items.filter(item => item.name.includes(filter));
    }, [items, filter]);

    // Mémorise la fonction
    const handleClick = useCallback((id) => {
        console.log('Clicked:', id);
    }, []);

    return (
        <ul>
            {filteredItems.map(item => (
                <li key={item.id} onClick={() => handleClick(item.id)}>
                    {item.name}
                </li>
            ))}
        </ul>
    );
}
```

### Custom Hooks
```jsx
function useLocalStorage(key, initialValue) {
    const [value, setValue] = useState(() => {
        const stored = localStorage.getItem(key);
        return stored ? JSON.parse(stored) : initialValue;
    });

    useEffect(() => {
        localStorage.setItem(key, JSON.stringify(value));
    }, [key, value]);

    return [value, setValue];
}

// Utilisation
function App() {
    const [theme, setTheme] = useLocalStorage('theme', 'light');
}
```

## Événements

```jsx
function Form() {
    const [value, setValue] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Submitted:', value);
    };

    const handleChange = (e) => {
        setValue(e.target.value);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={value}
                onChange={handleChange}
                placeholder="Entrez du texte"
            />
            <button type="submit">Envoyer</button>
        </form>
    );
}
```

## Rendu conditionnel

```jsx
function Greeting({ isLoggedIn, user }) {
    // Ternaire
    return isLoggedIn ? <UserGreeting user={user} /> : <GuestGreeting />;
}

function Notification({ message }) {
    // Short-circuit
    return message && <div className="notification">{message}</div>;
}

function Status({ status }) {
    // Switch avec objet
    const statusComponents = {
        loading: <Spinner />,
        error: <ErrorMessage />,
        success: <SuccessMessage />,
    };

    return statusComponents[status] || null;
}
```

## Listes et clés

```jsx
function TodoList({ todos }) {
    return (
        <ul>
            {todos.map(todo => (
                <li key={todo.id}>
                    {todo.text}
                </li>
            ))}
        </ul>
    );
}
```

## Formulaires contrôlés

```jsx
function ContactForm() {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        message: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(formData);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                name="name"
                value={formData.name}
                onChange={handleChange}
            />
            <input
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
            />
            <textarea
                name="message"
                value={formData.message}
                onChange={handleChange}
            />
            <button type="submit">Envoyer</button>
        </form>
    );
}
```

## Patterns courants

### Composition
```jsx
function Card({ children }) {
    return <div className="card">{children}</div>;
}

function CardHeader({ children }) {
    return <div className="card-header">{children}</div>;
}

function CardBody({ children }) {
    return <div className="card-body">{children}</div>;
}

// Utilisation
<Card>
    <CardHeader>Titre</CardHeader>
    <CardBody>Contenu</CardBody>
</Card>
```

### Render Props
```jsx
function DataFetcher({ url, render }) {
    const [data, setData] = useState(null);

    useEffect(() => {
        fetch(url)
            .then(res => res.json())
            .then(setData);
    }, [url]);

    return render(data);
}

// Utilisation
<DataFetcher
    url="/api/users"
    render={(data) => data ? <UserList users={data} /> : <Loading />}
/>
```

## Bonnes pratiques
- Garder les composants petits et focalisés
- Lever l'état au niveau approprié
- Utiliser des noms de props explicites
- Éviter les effets de bord dans le rendu
- Mémoriser les calculs coûteux avec useMemo
- Utiliser des clés stables et uniques pour les listes
