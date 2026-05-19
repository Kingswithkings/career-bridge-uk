import "./globals.css";
import Footer from "@/components/Footer";
import Navbar from "@/components/Navbar";

export const metadata = {
  title: "CareerBridge UK",
  description: "AI career mentor for UK job seekers",
  icons: {
    icon: "/icon.svg",
    shortcut: "/icon.svg",
    apple: "/icon.svg",
  },
  openGraph: {
    title: "CareerBridge UK",
    description: "AI career mentor for UK job seekers",
    images: [
      {
        url: "/opengraph-image.png",
        width: 1200,
        height: 630,
        alt: "CareerBridge UK book logo",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "CareerBridge UK",
    description: "AI career mentor for UK job seekers",
    images: ["/opengraph-image.png"],
  },
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
