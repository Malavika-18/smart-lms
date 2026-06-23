import { useEffect, useRef } from 'react';
import api from '../services/api';

const useTimeTracker = (pageName, courseId = null) => {
  const startTime = useRef(Date.now());
  const pageName_ = useRef(pageName);
  const courseId_ = useRef(courseId);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return;

    startTime.current = Date.now();
    pageName_.current = pageName;
    courseId_.current = courseId;

    const logTime = async () => {
      const duration = Math.floor((Date.now() - startTime.current) / 1000);
      if (duration < 5) return;
      try {
        await api.post('/timelog/log', {
          page_name: pageName_.current,
          duration_seconds: duration,
          course_id: courseId_.current
        });
      } catch {
        // Silently fail
      }
    };

    window.addEventListener('beforeunload', logTime);
    return () => {
      window.removeEventListener('beforeunload', logTime);
      logTime();
    };
  }, [pageName, courseId]);
};

export default useTimeTracker;