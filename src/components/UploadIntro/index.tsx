"use client";

import { motion } from "framer-motion";

export default function UploadIntro() {
  return (
    <section className="flex flex-col items-center justify-center text-center py-24 px-6 bg-gray-50">
      <motion.h3
        className="text-3xl md:text-5xl font-bold mb-6"
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 1 }}
      >
        지금 바로 나만의 폰트를 만들어 보세요
      </motion.h3>

      <motion.p
        className="text-lg text-gray-600 max-w-2xl mb-8"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ delay: 0.3, duration: 1 }}
      >
        업로드는 간단합니다. <br />
        글씨를 작성한 템플릿을 업로드하면 AI가 자동으로 처리해 줍니다.
      </motion.p>

      <motion.a
        href="upload"
        className="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg shadow hover:bg-blue-700"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ delay: 0.6, duration: 1 }}
      >
        시작하기
      </motion.a>
    </section>
  );
}
