import { forwardRef, InputHTMLAttributes } from "react"

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({
    label,
    error,
    className = "",
    ...props
  }, ref) => {
  return (
    <>
    { label && <label htmlFor={props.id} className="text-sm font-medium">{label}</label>}
    <input
      ref={ref}
      className={`w-full px-4 py-2 border rounded-lg outline-none transition-all duration-300 focus:ring-2 focus:ring-gray-800 focus:border-transparent placeholder:text-slate-400 ${
        error ? "border-red-500" : "border-slate-300"
      } ${className}`}
      {...props}
    />
    {error && <span className="text-red-500 text-sm">{error}</span>}
    </>
  )
}
);

Input.displayName = "Input";
export default Input;