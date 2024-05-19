import React, { useState } from "react";
import "./NewConnectionModal.css";
import Button from "../Button/Button";
import PersonAddAltIcon from "@mui/icons-material/PersonAddAlt";

const NewConnectionModal = () => {
  const [showModal, setShowModal] = useState<boolean>(false);
  const [userInfo, setUserInfo] = useState<string>("");
  const [users, setUsers] = useState<UserData[]>([]);

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    fetch("http://127.0.0.1:8000/users/suggest/" + e.target.value)
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        console.log(data);
        setUsers(data);
      });
  };

  const handleSubmitForm = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    fetch("http://127.0.0.1:8000/users/", {
      method: "post",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userInfo),
    })
      .then((response) => {
        setUserInfo("");
        setShowModal(false);
        return response.json();
      })
      .then((data) => console.log(data));
  };

  return (
    <>
      <Button onClick={() => setShowModal(true)} className="user-button">
        <PersonAddAltIcon fontSize="small" />
      </Button>
      {showModal ? (
        <div id="modal">
          <form onSubmit={handleSubmitForm}>
            <input
              type="text"
              placeholder="Email"
              onChange={handleEmailChange}
            ></input>
            <div className="buttons">
              <button onClick={() => setShowModal(false)} className="cancel">
                Cancel
              </button>
              <button type="submit" className="add">
                Add
              </button>
            </div>
          </form>
        </div>
      ) : null}
    </>
  );
};

export default NewConnectionModal;
