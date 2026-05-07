const { PHASE_DESTRUCTURE } = require('phaser');

module.exports = {
  experimental: {
    appDir: 'frontend',
  },
  buildCommand: 'npm run build',
  outputDirectory: 'dist',
  installCommand: 'npm install',
  devCommand: 'npm run dev',
  framework: null,
  rewrites: [
    {
      source: '/api/(.*)',
      destination: '/api/$1',
    },
    {
      source: '/(.*)',
      destination: '/index.html',
    },
  ],
};
