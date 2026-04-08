"use client";

import { useForm, SubmitHandler, RegisterOptions } from 'react-hook-form';

import Input from '@/components/Input';
import Button from '@/components/Button';


type AuthMode = 'login' | 'register';

export interface FormValues {
  email: string;
  password: string;
  name?: string;
  confirmPassword?: string;
}

interface AuthFormProps {
  mode: AuthMode;
  onSubmit: (data: FormValues) => void;
  isLoading?: boolean;
}

const AuthForm = ({
  mode,
  onSubmit,
  isLoading,
}: AuthFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch
  } = useForm<FormValues>();

  const password = watch("password");

  const getValidationRules = (field: keyof FormValues): RegisterOptions<FormValues, typeof field> => {
    if (mode === 'login') {
      if (field === 'email') return { required: "E-mail обязателен" };
      if (field === 'password') return { required: "Пароль обязателен" };
      
      return {};
    } else {
      switch(field) {
        case "email":
          return {
            required: "E-mail обязателен",
            pattern: {
              value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
              message: "Неверный формат e-mail",
            },
          };
        case "password":
          return {
            required: "Пароль обязателен",
            minLength: { value: 6, message: "Минимум 6 символов" },
          };
        case "name":
          return { required: "Имя обязательно" };
        case "confirmPassword":
          return {
            required: "Подтвердите пароль",
            validate: (value: string | undefined) => value === password || "Пароли не совпадают",
          };
        default:
          return {};
      }
    }
  }

  return (
    <>
    <form onSubmit={handleSubmit(onSubmit)} className='flex flex-col gap-2'>
      <Input
        id="email"
        label="E-mail"
        type="email"
        {...register("email", getValidationRules("email"))}
        error={errors.email?.message}
      />
      
      {mode === "register" && (
        <Input
          id="name"
          label="Имя"
          type="text"
          {...register("name", getValidationRules("name"))}
          error={errors.name?.message}
        />
      )}

      <Input
        id="password"
        label="Пароль"
        type="password"
        {...register("password", getValidationRules("password"))}
        error={errors.password?.message}
      />

      {mode === "register" && (
        <Input
          id="confirmPassword"
          label="Подтвердите пароль"
          type="password"
          {...register("confirmPassword", getValidationRules("confirmPassword"))}
          error={errors.confirmPassword?.message}
        />
      )}

      <Button>{mode === "login" ? "Войти" : "Зарегистрироваться"}</Button>
    </form>
    </>
  )
}

export default AuthForm;