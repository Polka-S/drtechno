import { ComponentPropsWithoutRef } from "react";

const Button = ({
  children,
  className = "",
  ...props
}: ComponentPropsWithoutRef<'button'>) => {
  return (
    <button
      {...props}
      className={`bg-gray-800 text-white cursor-pointer border rounded-xl w-full py-2 hover:bg-white hover:text-blue-950 transition-colors duration-300 disabled:opacity-50 disabled:hover:bg-gray-800 disabled:hover:text-white ${className}`}>
        {children ?? "Купить"}
    </button>
  )
}

export default Button;