import { ReactNode } from "react";
import "./Button.css";
interface ButtonProps {
  className?: string;
  children?: ReactNode;
  onClick: () => void;
}

const Button = ({ className, children, onClick }: ButtonProps) => {
  return (
    <button className={className} onClick={onClick} type="button">
      {children}
    </button>
  );
};

export default Button;
