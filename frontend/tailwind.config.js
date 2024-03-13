/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      height: {
        main: "calc(100vh - 44px)",
      },
      maxHeight: {
        main: "calc(100vh - 128px)",
      },
      fontSize: {
        xxs: ["10px", "14px"], // [font-size, line-height]
      },
      colors: {
        lgrn: "#dcfce7",
        grn: "#4ade80",
      },
    },
  },
  plugins: [],
}

