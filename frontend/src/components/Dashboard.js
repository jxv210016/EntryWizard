import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [unitSize, setUnitSize] = useState(0);
  const [taskStatus, setTaskStatus] = useState(false); // false for paused, true for running
  const token = 'your_token'; // Replace with actual token from authentication

  // Function to fetch unit size from the server
  const fetchUnitSize = async () => {
    try {
      const response = await axios.get('http://localhost:5000/get_unit_size', { headers: { Authorization: `Bearer ${token}` } });
      setUnitSize(response.data.unit_size);
    } catch (error) {
      console.error('Error fetching unit size:', error);
      // Handle errors appropriately
    }
  };

  // Function to fetch task status from the server
  const fetchTaskStatus = async () => {
    try {
      const response = await axios.get('http://localhost:5000/get_task_status', { headers: { Authorization: `Bearer ${token}` } });
      setTaskStatus(response.data.task_status);
    } catch (error) {
      console.error('Error fetching task status:', error);
      // Handle errors appropriately
    }
  };

  // Fetch unit size and task status on component mount
  useEffect(() => {
    fetchUnitSize();
    fetchTaskStatus();
  }, []);

  // Handle unit size change
  const handleUnitChange = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/unit', { unit_size: unitSize }, { headers: { Authorization: `Bearer ${token}` } });
      alert('Unit size updated successfully.');
    } catch (error) {
      console.error('Error updating unit size:', error);
      // Handle errors appropriately
    }
  };

  // Handle task toggle
  const toggleTask = async () => {
    try {
      const newStatus = !taskStatus;
      await axios.post('http://localhost:5000/toggle_task', { status: newStatus }, { headers: { Authorization: `Bearer ${token}` } });
      setTaskStatus(newStatus);
    } catch (error) {
      console.error('Error toggling task:', error);
      // Handle errors appropriately
    }
  };

  return (
    <div>
      <h1>Dashboard</h1>
      <form onSubmit={handleUnitChange}>
        <label>
          Unit Size:
          <input type="number" value={unitSize} onChange={(e) => setUnitSize(Number(e.target.value))} />
        </label>
        <button type="submit">Update Unit Size</button>
      </form>
      <button onClick={toggleTask}>{taskStatus ? 'Pause Task' : 'Start Task'}</button>
    </div>
  );
};

export default Dashboard;
