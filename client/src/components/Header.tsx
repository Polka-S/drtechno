"use client";

import Link from 'next/link';
import React, { useState } from 'react';
import { Search } from 'lucide-react';

import { poppins } from '@/lib/fonts';
import Nav from './Nav';


const Header = () => {
  const [searchValue, setSearchValue] = useState<string>("");

  const stylesContentInteractive: string = "md:gap-10 lg:gap-22" 

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchValue(e.target.value);
  }

  return (
    <header className="border-b border-white md:border-gray-300 fixed w-full top-0 left-0 bg-white">
      <div className="my-container">
        <div className={`content flex flex-col items-center justify-between py-2 gap-1 md:flex-row md:items-center ${stylesContentInteractive}`}>
          <div className="logo">
            <Link href="#" className='outline-0'>
              <h1 className={`gradient uppercase ${poppins.variable} font-bold`}>Dr Techno</h1>
            </Link>
          </div>
          <div className={`interactive flex-2 flex flex-row items-center justify-between gap-5 w-full ${stylesContentInteractive}`}>
            <div className="search flex-2 relative">
              <div className="search-icon absolute top-1/2 transform -translate-y-1/2 pl-2">
                <Search size={20} color='gray' />
              </div>
              <input
                className='rounded-md w-full p-1 pl-10 bg-gray-200 outline-0 md:p-1.5 md:pl-10'
                type="text"
                placeholder='Поиск...'
                value={searchValue}
                onChange={handleChange}
              />
            </div>
            <div className="buttons hidden md:flex flex-row justify-between gap-4 md:gap-6 lg:gap-8">
              <Nav showName={false} />
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;