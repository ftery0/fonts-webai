"use client";

interface HeaderProps {
  onTryClick: () => void;
}

export default function Header({ onTryClick }: HeaderProps) {
  return (
    <header className="fixed top-0 left-0 w-full flex justify-between items-center px-8 py-4 bg-white/70 backdrop-blur-md z-50">
      <h1 className="text-2xl font-bold">Font AI</h1>
      <button
        onClick={onTryClick}
        className="px-4 py-2 bg-black text-white rounded-xl hover:bg-gray-800 transition"
      >
        사용해보기
      </button>
    </header>
  );
}
