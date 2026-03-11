import React from 'react';

const TestPage = () => {
  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h1>🧪 Test Page</h1>
      <p>If you can see this page, React is working.</p>
      <div style={{ 
        background: '#f0f8ff', 
        padding: '20px', 
        borderRadius: '8px',
        margin: '20px 0'
      }}>
        <h2>Component Status</h2>
        <p>✅ React Components Loading</p>
        <p>✅ CSS Styles Applied</p>
        <p>✅ Navigation Working</p>
      </div>
    </div>
  );
};

export default TestPage;
