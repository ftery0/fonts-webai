"use client";

import { useState } from "react";
import Header from "@/components/Header";
import Landing from "@/components/Landing";
import UploadForm from "@/components/UploadForm";
import Feature from "@/components/Feature";
import UploadIntro from "@/components/UploadIntro";

export default function Home() {
  const [showUpload, setShowUpload] = useState(false);

  return (
    <div className="min-h-screen flex flex-col bg-white">
      <Header onTryClick={() => setShowUpload(true)} />

      {!showUpload ? (
        <>
          <section className="h-screen w-full flex items-center justify-center snap-start">
        <Landing />
      </section>
      <section className="h-screen w-full flex items-center justify-center snap-start">
        <Feature />
      </section>
           <section className="h-screen w-full flex items-center justify-center snap-start">
        <UploadIntro />
      </section>
        
      </>
      ) : (
        <main className="flex-1 flex flex-col items-center justify-center px-4">
          <h2 className="text-3xl font-bold mb-4">손글씨 업로드</h2>
          <UploadForm />
        </main>
      )}
    </div>
  );
}
