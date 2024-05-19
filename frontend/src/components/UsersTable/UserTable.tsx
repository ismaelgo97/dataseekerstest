import { useEffect, useState } from "react";
import "./UserTable.css";
import NewUserModal from "../NewUserModal/NewUserModal";
import DeleteIcon from "@mui/icons-material/Delete";
import Button from "../Button/Button";
import NewConnectionModal from "../NewConectionModal/NewConnectionModal";

const UserTable = () => {
  const [data, setData] = useState<UserData[]>([]);

  const fetchData = () => {
    fetch("http://127.0.0.1:8000/users/")
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        setData(data);
      });
  };

  const deleteUser = (id: number) => {
    fetch("http://127.0.0.1:8000/users/" + id, {
      method: "delete",
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => response.json())
      .then((data) => console.log(data))
      .finally(() => fetchData());
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <>
      <h1>All users</h1>
      <table>
        <thead>
          <tr>
            <th>Email</th>
            <th>Name</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
            <tr key={item.id}>
              <td>{item.email}</td>
              <td>{item.name}</td>
              <td>
                {
                  <>
                    <Button
                      className="delete-button"
                      onClick={() => deleteUser(item.id)}
                    >
                      <DeleteIcon fontSize="small" />
                    </Button>
                    <NewConnectionModal />
                  </>
                }
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <NewUserModal reloadData={fetchData} />
    </>
  );
};

export default UserTable;
