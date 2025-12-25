/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // Disable turbopack to avoid PostCSS issues with Tailwind
  experimental: {
    turbopack: process.env.NEXT_DISABLE_TURBOPACK === '1' ? false : true,
  },
};

module.exports = nextConfig;
