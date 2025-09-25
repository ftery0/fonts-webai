import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const formData = await req.formData();
  const file = formData.get("file") as File;
  const lang = (formData.get("lang") as string) || "kor";

  const backend = "http://localhost:8000/upload";
  const uploadForm = new FormData();
  uploadForm.append("file", file);
  uploadForm.append("lang", lang);

  const res = await fetch(backend, {
    method: "POST",
    body: uploadForm,
  });

  const data = await res.json();
  return NextResponse.json(data);
}
