import ChatAgent from "@/components/dashboard/chatAgent";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-white flex flex-col items-center justify-between p-4">
      <div className="w-full max-w-4xl text-center mb-8">
        <h1 className="text-5xl font-extrabold tracking-tight bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent">
          Talk2DB
        </h1>
        <p className="mt-4 text-slate-400 text-lg">
          Intelligent Text-to-SQL Business Intelligence Agent
        </p>
      </div>
      
      <ChatAgent />

      <footer className="mt-12 text-slate-500 text-sm">
        Built with Next.js, FastAPI, and LangChain
      </footer>
    </main>
  );
}