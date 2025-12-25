/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  experimental: {
    turbopack: false, // Disable turbopack to avoid PostCSS issues
  },
  webpack: (config) => {
    return config;
  },
};

module.exports = nextConfig;
