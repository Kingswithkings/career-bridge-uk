import "./globals.css";
import Footer from "@/components/Footer";
import Navbar from "@/components/Navbar";

export const metadata = {
  title: "CareerBridge UK",
  description: "AI career mentor for UK job seekers",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function () {
                try {
                  var savedMode = localStorage.getItem('theme-mode');
                  var mode = savedMode === 'light' || savedMode === 'dark' || savedMode === 'system'
                    ? savedMode
                    : 'system';
                  var theme = mode === 'system'
                    ? (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark')
                    : mode;
                  document.documentElement.dataset.themeMode = mode;
                  document.documentElement.dataset.theme = theme;
                } catch (_) {
                  document.documentElement.dataset.themeMode = 'system';
                  document.documentElement.dataset.theme = 'dark';
                }
              })();
            `,
          }}
        />
      </head>
      <body>
        <Navbar />
        {children}
        <Footer />
      </body>
    </html>
  );
}
