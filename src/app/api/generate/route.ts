import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const body = await req.json();
  const { text, lang } = body as { text: string; lang: string };

  const res = await fetch("http://localhost:8000/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, lang }),
    // Next.js 서버 라우트에서 외부 호출 타임아웃 기본값 회피를 위해
    cache: "no-store",
  });

  const data = await res.json();
  return NextResponse.json(data);
}


