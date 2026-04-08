"use client";

import { List, ShoppingCart, User, Heart } from "lucide-react";

import IconButton from "@/components/IconButton";
import { store } from "@/store/store";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { openAuthModal } from "@/store/slices/uiSlice";


interface NavProps {
  showName?: boolean
}

const Nav = ({
  showName = true
}: NavProps) => {
  const dispatch = useAppDispatch();
  const isAuthenticated  = useAppSelector((state) => state.auth.isAuthenticated);

  return (
    <>
    <IconButton
      icon={List}
      name='Каталог'
      href='/catalog'
      showName={showName}
    />
    <IconButton
      icon={ShoppingCart}
      name='Корзина'
      href='/cart'
      showName={showName}
    />
    <IconButton
      icon={Heart}
      name='Избранное'
      href='/'
      showName={showName}
    />
    {
      isAuthenticated ? (
        <IconButton
          icon={User}
          name='Профиль'
          href='/profile'
          showName={showName}
        />
      ) : (
        <IconButton
          icon={User}
          name='Профиль'
          onClick={() => dispatch(openAuthModal())}
          showName={showName}
        />
      )
    }
    </>
  )
};

export default Nav;