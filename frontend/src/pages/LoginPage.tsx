// Design source: /artifacts/97b3fc13e6a4_design/uiwireframes/wireframe_login_register.html
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export function LoginPage() {
  const navigate = useNavigate();
  const { login, register } = useAuth();

  // Login form state
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [loginError, setLoginError] = useState('');

  // Register form state
  const [registerFullName, setRegisterFullName] = useState('');
  const [registerEmail, setRegisterEmail] = useState('');
  const [registerPassword, setRegisterPassword] = useState('');
  const [registerConfirmPassword, setRegisterConfirmPassword] = useState('');
  const [agreeTerms, setAgreeTerms] = useState(false);
  const [registerSuccess, setRegisterSuccess] = useState('');
  const [registerError, setRegisterError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError('');
    
    try {
      await login({ email: loginEmail, password: loginPassword });
      navigate('/');
    } catch (err: any) {
      setLoginError(err.message || 'Invalid email or password. Please try again.');
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setRegisterError('');
    setRegisterSuccess('');

    if (registerPassword !== registerConfirmPassword) {
      setRegisterError('Passwords do not match');
      return;
    }

    if (!agreeTerms) {
      setRegisterError('You must agree to the Terms of Service');
      return;
    }

    try {
      await register({ full_name: registerFullName, email: registerEmail, password: registerPassword });
      setRegisterSuccess('Account created successfully! Please sign in.');
      // Clear form
      setRegisterFullName('');
      setRegisterEmail('');
      setRegisterPassword('');
      setRegisterConfirmPassword('');
      setAgreeTerms(false);
    } catch (err: any) {
      setRegisterError(err.message || 'Registration failed. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-purple-600 to-purple-800">
      <header className="bg-white/95 backdrop-blur border-b border-black/10 py-4 px-8">
        <div className="max-w-[1400px] mx-auto flex items-center justify-between">
          <Link to="/" className="text-[1.75rem] font-bold text-blue-600 no-underline">
            Smart Shop
          </Link>
          <Link to="/" className="text-gray-700 no-underline font-medium hover:text-blue-600">
            ← Back to Shopping
          </Link>
        </div>
      </header>

      <main className="flex-1 flex items-center justify-center py-12 px-8">
        <div className="bg-white rounded-2xl shadow-2xl max-w-[900px] w-full grid grid-cols-2 overflow-hidden">
          {/* Login Panel */}
          <div className="p-12">
            <h1 className="text-4xl font-bold mb-2 text-gray-900">Welcome Back</h1>
            <p className="text-gray-600 mb-8">Sign in to your account to continue shopping</p>

            {loginError && (
              <div className="bg-red-100 text-red-800 px-3 py-3 rounded-md text-sm mb-4">
                {loginError}
              </div>
            )}

            <form onSubmit={handleLogin}>
              <div className="mb-6">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  value={loginEmail}
                  onChange={(e) => setLoginEmail(e.target.value)}
                  placeholder="your@email.com"
                  className="w-full px-3.5 py-3.5 border-2 border-gray-300 rounded-lg text-base focus:outline-none focus:border-blue-600"
                  required
                />
              </div>

              <div className="mb-6">
                <label className="block text-sm font-semibold text-gray-700 mb-2">Password</label>
                <input
                  type="password"
                  value={loginPassword}
                  onChange={(e) => setLoginPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="w-full px-3.5 py-3.5 border-2 border-gray-300 rounded-lg text-base focus:outline-none focus:border-blue-600"
                  required
                />
              </div>

              <div className="flex items-center gap-2 mb-6">
                <input
                  type="checkbox"
                  id="remember"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="w-4.5 h-4.5 cursor-pointer"
                />
                <label htmlFor="remember" className="text-sm text-gray-700 cursor-pointer">
                  Remember me
                </label>
              </div>

              <button
                type="submit"
                className="w-full py-4 bg-blue-600 text-white border-none rounded-lg text-base font-semibold cursor-pointer hover:bg-blue-700 mb-4"
              >
                Sign In
              </button>

              <div className="text-center text-sm">
                <a href="#forgot" className="text-blue-600 no-underline hover:underline">
                  Forgot your password?
                </a>
              </div>
            </form>

            <div className="mt-6 pt-6 border-t border-gray-200">
              <div className="text-center text-sm text-gray-600 mb-4">Or sign in with</div>
              <div className="flex gap-4">
                <button className="flex-1 px-3 py-3 border-2 border-gray-300 bg-white rounded-lg font-semibold cursor-pointer flex items-center justify-center gap-2 hover:bg-gray-50">
                  🔵 Google
                </button>
                <button className="flex-1 px-3 py-3 border-2 border-gray-300 bg-white rounded-lg font-semibold cursor-pointer flex items-center justify-center gap-2 hover:bg-gray-50">
                  📘 Facebook
                </button>
              </div>
            </div>
          </div>

          {/* Divider */}
          <div className="w-px bg-gray-200"></div>

          {/* Register Panel */}
          <div className="p-12 bg-gray-50">
            <h1 className="text-4xl font-bold mb-2 text-gray-900">Create Account</h1>
            <p className="text-gray-600 mb-8">Join Smart Shop to start shopping</p>

            {registerSuccess && (
              <div className="bg-green-100 text-green-800 px-3 py-3 rounded-md text-sm mb-4">
                {registerSuccess}
              </div>
            )}

            {registerError && (
              <div className="bg-red-100 text-red-800 px-3 py-3 rounded-md text-sm mb-4">
                {registerError}
              </div>
            )}

            <form onSubmit={handleRegister}>
              <div className="mb-6">
                <label className="block text-sm font-semibold text-gray-700 mb-2">Full Name</label>
                <input
                  type="text"
                  value={registerFullName}
                  onChange={(e) => setRegisterFullName(e.target.value)}
                  placeholder="John Smith"
                  className="w-full px-3.5 py-3.5 border-2 border-gray-300 rounded-lg text-base focus:outline-none focus:border-blue-600"
                  required
                />
              </div>

              <div className="mb-6">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  value={registerEmail}
                  onChange={(e) => setRegisterEmail(e.target.value)}
                  placeholder="your@email.com"
                  className="w-full px-3.5 py-3.5 border-2 border-gray-300 rounded-lg text-base focus:outline-none focus:border-blue-600"
                  required
                />
              </div>

              <div className="mb-6">
                <label className="block text-sm font-semibold text-gray-700 mb-2">Password</label>
                <input
                  type="password"
                  value={registerPassword}
                  onChange={(e) => setRegisterPassword(e.target.value)}
                  placeholder="Create a password"
                  className="w-full px-3.5 py-3.5 border-2 border-gray-300 rounded-lg text-base focus:outline-none focus:border-blue-600"
                  required
                />
                <div className="text-xs text-gray-600 mt-2">
                  Must be at least 8 characters with uppercase, lowercase, and number
                </div>
              </div>

              <div className="mb-6">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Confirm Password
                </label>
                <input
                  type="password"
                  value={registerConfirmPassword}
                  onChange={(e) => setRegisterConfirmPassword(e.target.value)}
                  placeholder="Confirm your password"
                  className="w-full px-3.5 py-3.5 border-2 border-gray-300 rounded-lg text-base focus:outline-none focus:border-blue-600"
                  required
                />
              </div>

              <div className="flex items-center gap-2 mb-6">
                <input
                  type="checkbox"
                  id="terms"
                  checked={agreeTerms}
                  onChange={(e) => setAgreeTerms(e.target.checked)}
                  className="w-4.5 h-4.5 cursor-pointer"
                />
                <label htmlFor="terms" className="text-sm text-gray-700 cursor-pointer">
                  I agree to the Terms of Service and Privacy Policy
                </label>
              </div>

              <button
                type="submit"
                className="w-full py-4 bg-blue-600 text-white border-none rounded-lg text-base font-semibold cursor-pointer hover:bg-blue-700"
              >
                Create Account
              </button>
            </form>

            <div className="mt-6 pt-6 border-t border-gray-200">
              <div className="text-center text-sm text-gray-600 mb-4">Or register with</div>
              <div className="flex gap-4">
                <button className="flex-1 px-3 py-3 border-2 border-gray-300 bg-white rounded-lg font-semibold cursor-pointer flex items-center justify-center gap-2 hover:bg-gray-50">
                  🔵 Google
                </button>
                <button className="flex-1 px-3 py-3 border-2 border-gray-300 bg-white rounded-lg font-semibold cursor-pointer flex items-center justify-center gap-2 hover:bg-gray-50">
                  📘 Facebook
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
