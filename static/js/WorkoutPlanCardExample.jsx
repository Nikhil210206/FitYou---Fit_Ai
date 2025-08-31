import React from 'react';
import WorkoutPlanCard from './WorkoutPlanCard';

// Example usage of the WorkoutPlanCard component
const WorkoutPlanCardExample = () => {
  const handleDaySelect = (dayId) => {
    console.log(`Selected day: ${dayId}`);
    // You can add navigation logic here
    // For example: navigate to `/workout/day${dayId}` or `/GP/day${dayId}`
  };

  const handleStartWorkout = (dayId) => {
    console.log(`Starting workout for day: ${dayId}`);
    // You can add workout start logic here
    // For example: navigate to workout session page
  };

  return (
    <div>
      {/* Basic Usage */}
      <WorkoutPlanCard 
        onDaySelect={handleDaySelect}
        onStartWorkout={handleStartWorkout}
      />

      {/* Custom Title and Subtitle */}
      <WorkoutPlanCard 
        title="Custom Workout Plan"
        subtitle="Tailored fitness routine for your goals"
        onDaySelect={handleDaySelect}
        onStartWorkout={handleStartWorkout}
      />

      {/* Minimal Props */}
      <WorkoutPlanCard />
    </div>
  );
};

export default WorkoutPlanCardExample;
