// frontend/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  // swcMinify est maintenant activé par défaut dans Next.js 15, on peut le retirer
}

module.exports = nextConfig
