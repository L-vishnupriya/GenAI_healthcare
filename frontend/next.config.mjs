/** @type {import('next').NextConfig} */
const nextConfig = {
    // Required for optimizing the output directory for Docker deployment.
    // This creates a minimal folder structure for the "runner" stage in the Dockerfile.
    output: 'standalone',
  
    // Optional: Set a specific base path if the app is hosted under a subdirectory.
    // basePath: '', 
  
    // Add any other specific configurations here if needed, 
    // such as image domains or compiler options.
  };
  
  export default nextConfig;