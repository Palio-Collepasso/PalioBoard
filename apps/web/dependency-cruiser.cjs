/** @type {import('dependency-cruiser').IConfiguration} */
module.exports = {
  forbidden: [
    {
      name: 'no-admin-shell-imports-from-other-shells',
      comment: 'Admin shell code must stay isolated from public and maxi shell code.',
      severity: 'error',
      from: { path: '^src/app/shell-admin/' },
      to: { path: '^src/app/shell-(public|maxi)/' }
    },
    {
      name: 'no-public-shell-imports-from-other-shells',
      comment: 'Public shell code must stay isolated from admin and maxi shell code.',
      severity: 'error',
      from: { path: '^src/app/shell-public/' },
      to: { path: '^src/app/shell-(admin|maxi)/' }
    },
    {
      name: 'no-maxi-shell-imports-from-other-shells',
      comment: 'Maxi shell code must stay isolated from admin and public shell code.',
      severity: 'error',
      from: { path: '^src/app/shell-maxi/' },
      to: { path: '^src/app/shell-(admin|public)/' }
    },
    {
      name: 'no-feature-to-shell-imports',
      comment: 'Features should stay reusable inside a shell route and not depend on shell chrome.',
      severity: 'error',
      from: { path: '^src/app/features/' },
      to: { path: '^src/app/shell-(admin|public|maxi)/' }
    },
    {
      name: 'shared-must-stay-generic',
      comment: 'Shared code cannot depend on core, features, or shell-specific areas.',
      severity: 'error',
      from: { path: '^src/app/shared/' },
      to: { path: '^src/app/(core|features|shell-admin|shell-public|shell-maxi)/' }
    },
    {
      name: 'core-must-stay-cross-cutting',
      comment: 'Core can depend on shared building blocks, but not on shells or features.',
      severity: 'error',
      from: { path: '^src/app/core/' },
      to: { path: '^src/app/(features|shell-admin|shell-public|shell-maxi)/' }
    }
  ],
  options: {
    tsConfig: {
      fileName: 'tsconfig.app.json'
    },
    doNotFollow: {
      path: 'node_modules'
    }
  }
};
