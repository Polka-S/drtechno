import Nav from "./Nav";


const MobileNav = () => {
  return (
    <div className="my-container">
      <div className="nav-mobile z-10 bg-white md:hidden shadow-2xl shadow-amber-950 fixed bottom-0 right-0 w-full flex justify-between px-10 py-2">
          <Nav showName={true}/>
      </div>
    </div>
  );
};

export default MobileNav;