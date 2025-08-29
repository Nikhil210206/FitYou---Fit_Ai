# WorkoutPlanCard Component

A responsive React component for displaying workout plans with interactive day selection, built with Tailwind CSS and full dark/light mode support.

## Features

- ✅ **Responsive Design**: Mobile-first approach with responsive breakpoints
- ✅ **Dark/Light Mode**: Seamless theme switching with Tailwind's `dark:` variants
- ✅ **Interactive Day Selection**: Clickable chips for Day 1-4 with active states
- ✅ **Modern UI**: Clean design with rounded corners, shadows, and smooth transitions
- ✅ **Accessibility**: Proper ARIA attributes and keyboard navigation
- ✅ **TypeScript Support**: Full type safety with TypeScript definitions
- ✅ **Customizable**: Configurable title, subtitle, and callback functions

## Design Specifications

### Light Mode
- **Background**: White (`bg-white`)
- **Borders**: Soft gray (`border-gray-200`)
- **Text**: Dark gray (`text-gray-900`)
- **Highlights**: Blue (`bg-blue-500`)
- **Shadows**: Subtle gray shadows

### Dark Mode
- **Background**: Dark gray (`dark:bg-gray-800`)
- **Borders**: Lighter gray (`dark:border-gray-700`)
- **Text**: White (`dark:text-white`)
- **Highlights**: Vibrant blue (`dark:bg-blue-600`)
- **Shadows**: Enhanced dark shadows

### Layout
- **Container**: Centered with `max-w-md` width
- **Padding**: `p-6` for card content
- **Border Radius**: `rounded-2xl` for modern look
- **Spacing**: Consistent gap system using Tailwind spacing

## Installation

1. Ensure you have React and Tailwind CSS installed
2. Copy the component files to your project
3. Import and use the component

## Usage

### Basic Usage

```jsx
import WorkoutPlanCard from './WorkoutPlanCard';

function App() {
  return <WorkoutPlanCard />;
}
```

### With Custom Props

```jsx
import WorkoutPlanCard from './WorkoutPlanCard';

function App() {
  const handleDaySelect = (dayId) => {
    console.log(`Selected day: ${dayId}`);
    // Navigate to specific day workout
  };

  const handleStartWorkout = (dayId) => {
    console.log(`Starting workout for day: ${dayId}`);
    // Start workout session
  };

  return (
    <WorkoutPlanCard 
      title="Custom Workout Plan"
      subtitle="Tailored fitness routine for your goals"
      onDaySelect={handleDaySelect}
      onStartWorkout={handleStartWorkout}
    />
  );
}
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `string` | `"4-Day Workout Plan"` | The main title of the workout plan |
| `subtitle` | `string` | `"Personalized strength and endurance routine"` | The subtitle/description |
| `onDaySelect` | `(dayId: number) => void` | `undefined` | Callback when a day is selected |
| `onStartWorkout` | `(dayId: number) => void` | `undefined` | Callback when start workout is clicked |

## Component Structure

```
WorkoutPlanCard
├── Container (min-h-screen, centered)
├── Card (rounded-2xl, shadow, border)
│   ├── Header (title + subtitle)
│   ├── Day Selection Chips (flex, gap-3)
│   ├── Selected Day Info (bg-gray-50)
│   └── Action Button (full-width)
```

## Styling Classes

### Card Container
- `bg-white dark:bg-gray-800`
- `rounded-2xl`
- `p-6`
- `shadow-lg dark:shadow-xl`
- `border border-gray-200 dark:border-gray-700`

### Day Chips
- **Active**: `bg-blue-500 text-white shadow-md transform scale-105`
- **Inactive**: `bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300`
- **Hover**: `hover:bg-gray-200 dark:hover:bg-gray-600`

### Typography
- **Title**: `text-2xl font-bold`
- **Subtitle**: `text-sm font-medium`
- **Info Text**: `text-sm`

## Accessibility Features

- Proper ARIA attributes (`aria-pressed`)
- Focus management with visible focus rings
- Keyboard navigation support
- Semantic HTML structure
- Color contrast compliance

## Browser Support

- Modern browsers with CSS Grid and Flexbox support
- Tailwind CSS v3.0+
- React 16.8+ (for hooks)

## Customization

### Adding More Days

```jsx
// Modify the days array in the component
const days = [
  { id: 1, label: "Day 1" },
  { id: 2, label: "Day 2" },
  { id: 3, label: "Day 3" },
  { id: 4, label: "Day 4" },
  { id: 5, label: "Day 5" }, // Add more days
  { id: 6, label: "Day 6" },
];
```

### Custom Colors

Override Tailwind classes or modify the component to use custom color variables:

```jsx
// Example with custom colors
className="bg-custom-primary dark:bg-custom-primary-dark"
```

## Integration with Navigation

To integrate with your routing system (React Router, Next.js, etc.):

```jsx
import { useNavigate } from 'react-router-dom';

function WorkoutPage() {
  const navigate = useNavigate();

  const handleDaySelect = (dayId) => {
    navigate(`/workout/day${dayId}`);
  };

  const handleStartWorkout = (dayId) => {
    navigate(`/workout/session/${dayId}`);
  };

  return (
    <WorkoutPlanCard 
      onDaySelect={handleDaySelect}
      onStartWorkout={handleStartWorkout}
    />
  );
}
```

## Performance Considerations

- Component uses `useState` for local state management
- Minimal re-renders with proper dependency arrays
- Optimized Tailwind classes for production builds
- No external dependencies beyond React

## Troubleshooting

### Dark Mode Not Working
- Ensure Tailwind's dark mode is configured in `tailwind.config.js`
- Check if the parent element has `dark` class or `data-theme="dark"`

### Styling Issues
- Verify Tailwind CSS is properly imported
- Check for conflicting CSS classes
- Ensure proper CSS purging in production builds

### Responsive Issues
- Test on different screen sizes
- Verify viewport meta tag is set correctly
- Check for conflicting responsive utilities
