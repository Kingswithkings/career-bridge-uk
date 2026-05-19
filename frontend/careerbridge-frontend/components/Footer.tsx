import Link from "next/link";

const companyUrl = process.env.NEXT_PUBLIC_COMPANY_URL || "https://1st-kings.com";

export default function Footer() {
  return (
    <footer className="border-t border-slate-800 bg-slate-950 px-6 py-6 text-sm text-slate-400">
      <div className="mx-auto flex max-w-6xl flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <p>CareerBridge UK © 2026</p>
        <div className="flex flex-wrap gap-x-5 gap-y-2">
          <a href={companyUrl} target="_blank" rel="noreferrer" className="hover:text-white">
            Powered by 1stKings
          </a>
          <Link href="/feedback" className="hover:text-white">
            Feedback
          </Link>
          <a href="mailto:kings@1st-kings.com" className="hover:text-white">
            Contact
          </a>
        </div>
      </div>
    </footer>
  );
}
