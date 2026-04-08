import Link from "next/link";
import { LucideIcon } from "lucide-react";
import { ComponentPropsWithoutRef } from "react";


type IconButtonProps = {
  icon: LucideIcon;
  iconSize?: number;
  name?: string;
  showName?: boolean;
  className?: string;
  wrapperClassName?: string;
} & (
  | { href: string; onClick?: never; } & ComponentPropsWithoutRef<'a'>
  | { href?: never; onClick: () => void; } & ComponentPropsWithoutRef<'button'>
)

const IconButton = ({
  icon: Icon,
  iconSize = 24,
  name,
  href,
  showName = true,
  className = "",
  wrapperClassName = "",
  onClick,
  ...props
}: IconButtonProps) => {
  const generalStyle = "rounded-sm hover:text-blue-900 transition-colors duration-300 cursor-pointer";

  const content = (
    <div className={`button flex flex-col items-center justify-start ${wrapperClassName}`}>
      <Icon size={iconSize}/>
      { showName && <p className="text-sm">{name}</p> }
    </div>
  )

  const combinedClassName = `${generalStyle} ${className}`.trim();

  if (href) {
    const { ...anchorProps } = props as ComponentPropsWithoutRef<'a'>;
    return (
      <Link href={href} className={combinedClassName} {...anchorProps}>
        {content}
      </Link>
    );
  }

  if (onClick) {
    const { ...anchorProps } = props as ComponentPropsWithoutRef<'button'>;
    return (
      <button onClick={onClick} className={combinedClassName} {...anchorProps}>
        {content}
      </button>
    );
  }

  return null;
};

export default IconButton;