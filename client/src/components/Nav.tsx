import NavButton from "./NavButton"
import { List, ShoppingCart, User, Heart } from "lucide-react";


interface NavProps {
  showName?: boolean
}

const Nav = ({
  showName = true
}: NavProps) => {
  return (
    <>
    <NavButton
      icon={List}
      name='Каталог'
      href='/catalog'
      showName={showName}
    />
    <NavButton
      icon={ShoppingCart}
      name='Корзина'
      href='/cart'
      showName={showName}
    />
    <NavButton
      icon={Heart}
      name='Избранное'
      href='/'
      showName={showName}
    />
    <NavButton
      icon={User}
      name='Профиль'
      href='/login'
      showName={showName}
    />
    </>
  )
};

export default Nav;