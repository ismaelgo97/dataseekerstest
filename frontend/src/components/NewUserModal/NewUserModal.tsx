import React, { useState } from "react";
import "./NewUserModal.css";
import Button from "../Button/Button";
import AddIcon from "@mui/icons-material/Add";

interface NewUserModalProps {
  reloadData: () => void;
}

const NewUserModal = ({ reloadData }: NewUserModalProps) => {
  const [showModal, setShowModal] = useState<boolean>(false);
  const [userInfo, setUserInfo] = useState<UserDataCreate>({
    email: "",
    name: "",
  });

  const openUserModal = () => {
    setShowModal(true);
  };

  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUserInfo((prev) => {
      return { ...prev, name: e.target.value };
    });
  };

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUserInfo((prev) => {
      return { ...prev, email: e.target.value };
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
        setUserInfo({ name: "", email: "" });
        setShowModal(false);
        reloadData();
        return response.json();
      })
      .then((data) => console.log(data));
  };

  return (
    <>
      <div className="button-wrapper">
        <Button onClick={openUserModal} className="user-button">
          <AddIcon />
          Add user
        </Button>
      </div>
      {showModal ? (
        <div id="modal">
          <form onSubmit={handleSubmitForm}>
            <input
              type="text"
              placeholder="Email"
              onChange={handleEmailChange}
            ></input>

            <input
              type="text"
              placeholder="Name"
              onChange={handleNameChange}
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

export default NewUserModal;
