module.exports = {
  apps: [{
    name: '{{APP_NAME}}',
    script: 'build/index.js',  // or 'server.js' for plain Node
    interpreter: '/opt/bin/node',
    cwd: '/share/CACHEDEV1_DATA/Container/caddy/apps/{{SUBDOMAIN}}.jurrejan.com',
    env: {
      NODE_ENV: 'production',
      PORT: {{PORT}}
    }
  }]
}
