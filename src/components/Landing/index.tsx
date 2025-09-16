"use client";

import { motion } from "framer-motion";

export default function Landing() {
  return (
    <main className="flex-1 flex flex-col items-center justify-center text-center px-4">
      <motion.h2
        className="text-5xl md:text-7xl font-extrabold mb-6"
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
      >
        나만의 글씨체, <br /> 디지털 폰트로 변환하세요
      </motion.h2>

      <motion.p
        className="text-lg md:text-xl text-gray-600 max-w-2xl"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5, duration: 1 }}
      >
        종이에 쓴 글씨를 업로드하면, 인공지능이 당신만의 글씨체를 분석해
        <br />
        고유한 디지털 폰트로 만들어 드립니다.
      </motion.p>

      <motion.div
        className="mt-16"
        initial={{ opacity: 0, y: 100 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1, duration: 1 }}
      >
        <svg
          className="w-6 h-6 animate-bounce text-gray-400"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </motion.div>
    </main>
  );
}
