import { useState } from 'react';

export default function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="card mx-auto" style={{ maxWidth: '420px' }}>
      <div className="card-body">
        <h2 className="card-title">React Counter</h2>
        <p className="card-text">This section is rendered with React and Vite.</p>
        <div className="d-flex align-items-center justify-content-between">
          <button className="btn btn-primary" onClick={() => setCount((value) => value - 1)}>-</button>
          <span className="fs-4 mb-0">{count}</span>
          <button className="btn btn-primary" onClick={() => setCount((value) => value + 1)}>+</button>
        </div>
      </div>
    </div>
  );
}
