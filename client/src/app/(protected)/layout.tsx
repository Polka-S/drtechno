import Header from "@/components/Header";
import MobileNav from "@/components/MobileNav";

export default function MainLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="">
      <Header />
      { children }
      <MobileNav />
    </div>
  )
}