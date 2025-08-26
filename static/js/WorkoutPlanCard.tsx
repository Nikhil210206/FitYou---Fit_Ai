import React, { useState } from 'react';

interface WorkoutPlanCardProps {
  title?: string;
  subtitle?: string;
  onDaySelect?: (dayId: number) => void;
  onStartWorkout?: (dayId: number) => void;
}

interface Day {
  id: number;
  label: string;
}

const WorkoutPlanCard: React.FC<WorkoutPlanCardProps> = ({ 
  title = "4-Day Workout Plan", 
  subtitle = "Personalized strength and endurance routine",
  onDaySelect,
  onStartWorkout
}) => {
  const [selectedDay, setSelectedDay] = useState<number>(1);

  const days: Day[] = [
    { id: 1, label: "Day 1" },
    { id: 2, label: "Day 2" },
    { id: 3, label: "Day 3" },
    { id: 4, label: "Day 4" }
  ];

  const handleDaySelect = (dayId: number) => {
    setSelectedDay(dayId);
    onDaySelect?.(dayId);
  };

  const handleStartWorkout = () => {
    onStartWorkout?.(selectedDay);
  };

  const selectedDayData = days.find(day => day.id === selectedDay);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Workout Plan Card */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg dark:shadow-xl border border-gray-200 dark:border-gray-700 transition-all duration-300 hover:shadow-xl dark:hover:shadow-2xl">
          
          {/* Card Header */}
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              {title}
            </h2>
            <p className="text-gray-600 dark:text-gray-300 text-sm font-medium">
              {subtitle}
            </p>
          </div>

          {/* Day Selection Chips */}
          <div className="flex flex-wrap gap-3 justify-center">
            {days.map((day) => (
              <button
                key={day.id}
                onClick={() => handleDaySelect(day.id)}
                className={`
                  px-4 py-2 rounded-xl font-medium text-sm transition-all duration-200
                  ${selectedDay === day.id
                    ? 'bg-blue-500 text-white shadow-md transform scale-105'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                  }
                  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800
                `}
                aria-pressed={selectedDay === day.id}
              >
                {day.label}
              </button>
            ))}
          </div>

          {/* Selected Day Info */}
          <div className="mt-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-xl">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
              {selectedDayData?.label} Workout
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              Your personalized workout routine for {selectedDayData?.label.toLowerCase()}
            </p>
          </div>

          {/* Action Button */}
          <div className="mt-6">
            <button 
              onClick={handleStartWorkout}
              className="w-full bg-blue-500 hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-xl transition-all duration-200 transform hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
            >
              Start {selectedDayData?.label} Workout
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WorkoutPlanCard;
