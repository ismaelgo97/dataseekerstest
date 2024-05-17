import { useEffect, useState } from "react";
import "./App.css";

function App() {
  interface UserData {
    id: number;
    email: string;
    name: string;
  }

  const [data, setData] = useState<UserData[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/users/")
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        console.log(data);
        setData(data);
      });
  }, []);

  return (
    <>
      <h1>Hello!</h1>
      {data.map((user) => (
        <div className="column">
          <p className="delimiter">{user.id}</p>
          <p className="delimiter">{user.email}</p>
          <p>{user.name}</p>
        </div>
      ))}
    </>
  );
}

export default App;
