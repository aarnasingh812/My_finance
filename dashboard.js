// src/Dashboard.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const [salary, setSalary] = useState('');
  const [banks, setBanks] = useState(['']);
  const [occupation, setOccupation] = useState('');
  const navigate = useNavigate();

  const handleBankChange = (index, value) => {
    const updatedBanks = [...banks];
    updatedBanks[index] = value;
    setBanks(updatedBanks);
  };

  const addBankField = () => {
    setBanks([...banks, '']);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const userData = {
      salary,
      banks: banks.filter(b => b !== ''),
      occupation
    };
    console.log("User Financial Info:", userData);
    // Optionally store in localStorage or send to backend
    // localStorage.setItem('userData', JSON.stringify(userData));
    alert("Details saved!");
    // navigate('/next'); // Optional next page
  };

  return (
    <div style={{ maxWidth: '500px', margin: 'auto', padding: '20px' }}>
      <h2>Welcome to Your Dashboard</h2>
      <div style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '10px' }}>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Salary:</label>
            <input
              type="number"
              value={salary}
              onChange={(e) => setSalary(e.target.value)}
              required
            />
          </div>

          <div>
            <label>Bank Balances:</label>
            {banks.map((bank, index) => (
              <input
                key={index}
                type="number"
                placeholder={`Bank ${index + 1}`}
                value={bank}
                onChange={(e) => handleBankChange(index, e.target.value)}
                required
              />
            ))}
            <button type="button" onClick={addBankField}>+ Add Bank</button>
          </div>

          <div>
            <label>Occupation:</label>
            <input
              type="text"
              value={occupation}
              onChange={(e) => setOccupation(e.target.value)}
              required
            />
          </div>

          <button type="submit">Save & Continue</button>
        </form>
      </div>
    </div>
  );
}

export default Dashboard;
