import { LucideIcon } from "lucide-react";
import Link from "next/link";

interface NavButtonProps {
  icon: LucideIcon;
  name?: string;
  href: string;
  showName?: boolean;
}

const NavButton = ({
  icon: Icon,
  name,
  href,
  showName = true,
}: NavButtonProps) => {
  return (
    <Link href={href} className="rounded-sm hover:text-blue-900 transition-colors duration-300">
      <div className="button flex flex-col items-center justify-start">
        <Icon size={24}/>
        { showName && <p className="text-sm">{name}</p> }
      </div>
    </Link>
  );
};

export default NavButton;