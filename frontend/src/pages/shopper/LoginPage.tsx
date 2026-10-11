import { useState, FormEvent } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authService } from '../../services/auth';
import { useAuth } from '../../lib/auth-context';
import sharedConfig from '../../../shared_config.json';

export function LoginPage() {
  const navigate = useNavigate();
  const { login: authLogin } = useAuth();
  const [loginForm, setLoginForm] = useState({
    email: 'admin@example.com',
    password: 'admin123',
  });
  const [registerForm, setRegisterForm] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    agreeToTerms: false,
  });
  const [loginError, setLoginError] = useState('');
  const [registerError, setRegisterError] = useState('');
  const [loginLoading, setLoginLoading] = useState(false);
  const [registerLoading, setRegisterLoading] = useState(false);

  const handleLogin = async (e: FormEvent) => {
    e.preventDefault();
    setLoginError('');
    setLoginLoading(true);

    try {
      await authLogin({
        email: loginForm.email,
        password: loginForm.password,
      });
      navigate('/');
    } catch (err: any) {
      setLoginError(err.message || 'Login failed');
    } finally {
      setLoginLoading(false);
    }
  };

  const handleRegister = async (e: FormEvent) => {
    e.preventDefault();
    setRegisterError('');

    if (registerForm.password !== registerForm.confirmPassword) {
      setRegisterError('Passwords do not match');
      return;
    }

    if (!registerForm.agreeToTerms) {
      setRegisterError('You must agree to the Terms of Service and Privacy Policy');
      return;
    }

    setRegisterLoading(true);

    try {
      await authService.register({
        name: registerForm.name,
        email: registerForm.email,
        password: registerForm.password,
      });
      // After successful registration, log in
      await authLogin({
        email: registerForm.email,
        password: registerForm.password,
      });
      navigate('/');
    } catch (err: any) {
      setRegisterError(err.message || 'Registration failed');
    } finally {
      setRegisterLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#FAFAFA]">
      {/* Header */}
      <header className="bg-white border-b border-[#E5E5E5] py-4 px-6">
        <div className="max-w-[1440px] mx-auto flex items-center justify-center">
          <Link to="/" className="text-2xl font-bold text-[#0066FF]">
            Smart Shop
          </Link>
        </div>
      </header>

      {/* Auth Container */}
      <div className="max-w-[1200px] mx-auto py-12 px-6 grid grid-cols-1 md:grid-cols-2 gap-12">
        {/* Sign In Card */}
        <div className="bg-white border border-[#E5E5E5] rounded-xl p-10">
          <h1 className="text-3xl font-bold mb-2">Sign In</h1>
          <p className="text-[#666] mb-8 text-[15px]">Welcome back! Sign in to your account</p>

          <form onSubmit={handleLogin}>
            <div className="mb-5">
              <label htmlFor="login-email" className="block text-sm font-semibold mb-2">Email Address</label>
              <input
                id="login-email"
                type="email"
                className="w-full py-3 px-3 border border-[#D1D1D1] rounded-md text-[15px] focus:outline-none focus:border-[#0066FF]"
                placeholder="your@email.com"
                value={loginForm.email}
                onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })}
                required
              />
            </div>

            <div className="mb-5">
              <label htmlFor="login-password" className="block text-sm font-semibold mb-2">Password</label>
              <input
                id="login-password"
                type="password"
                className="w-full py-3 px-3 border border-[#D1D1D1] rounded-md text-[15px] focus:outline-none focus:border-[#0066FF]"
                placeholder="Enter your password"
                value={loginForm.password}
                onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                required
              />
            </div>

            <div className="text-right mb-6">
              <a href="#" className="text-[#0066FF] text-sm">
                Forgot password?
              </a>
            </div>

            {loginError && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-md">
                {loginError}
              </div>
            )}

            <button
              type="submit"
              disabled={loginLoading}
              className="w-full py-3.5 bg-[#0066FF] text-white rounded-lg text-base font-semibold mb-4 hover:bg-[#0052CC] disabled:opacity-50"
            >
              {loginLoading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <div className="flex items-center my-6 text-[#666] text-sm">
            <div className="flex-1 border-b border-[#E5E5E5]"></div>
            <span className="px-4">or continue with</span>
            <div className="flex-1 border-b border-[#E5E5E5]"></div>
          </div>

          <button className="w-full py-3 bg-white border border-[#D1D1D1] rounded-lg text-[15px] font-medium mb-3 flex items-center justify-center gap-2 hover:bg-[#F5F5F5]">
            <span>🔵</span>
            Continue with Google
          </button>

          <button className="w-full py-3 bg-white border border-[#D1D1D1] rounded-lg text-[15px] font-medium flex items-center justify-center gap-2 hover:bg-[#F5F5F5]">
            <span>📘</span>
            Continue with Facebook
          </button>
        </div>

        {/* Register Card */}
        <div className="bg-white border border-[#E5E5E5] rounded-xl p-10">
          <h1 className="text-3xl font-bold mb-2">Create Account</h1>
          <p className="text-[#666] mb-8 text-[15px]">Join Smart Shop and start shopping</p>

          <form onSubmit={handleRegister}>
            <div className="mb-5">
              <label htmlFor="register-name" className="block text-sm font-semibold mb-2">Full Name</label>
              <input
                id="register-name"
                type="text"
                className="w-full py-3 px-3 border border-[#D1D1D1] rounded-md text-[15px] focus:outline-none focus:border-[#0066FF]"
                placeholder="John Smith"
                value={registerForm.name}
                onChange={(e) => setRegisterForm({ ...registerForm, name: e.target.value })}
                required
              />
            </div>

            <div className="mb-5">
              <label htmlFor="register-email" className="block text-sm font-semibold mb-2">Email Address</label>
              <input
                id="register-email"
                type="email"
                className="w-full py-3 px-3 border border-[#D1D1D1] rounded-md text-[15px] focus:outline-none focus:border-[#0066FF]"
                placeholder="your@email.com"
                value={registerForm.email}
                onChange={(e) => setRegisterForm({ ...registerForm, email: e.target.value })}
                required
              />
            </div>

            <div className="mb-5">
              <label htmlFor="register-password" className="block text-sm font-semibold mb-2">Password</label>
              <input
                id="register-password"
                type="password"
                className="w-full py-3 px-3 border border-[#D1D1D1] rounded-md text-[15px] focus:outline-none focus:border-[#0066FF]"
                placeholder="Create a password"
                value={registerForm.password}
                onChange={(e) => setRegisterForm({ ...registerForm, password: e.target.value })}
                required
              />
            </div>

            <div className="mb-5">
              <label htmlFor="register-confirm-password" className="block text-sm font-semibold mb-2">Confirm Password</label>
              <input
                id="register-confirm-password"
                type="password"
                className="w-full py-3 px-3 border border-[#D1D1D1] rounded-md text-[15px] focus:outline-none focus:border-[#0066FF]"
                placeholder="Confirm your password"
                value={registerForm.confirmPassword}
                onChange={(e) =>
                  setRegisterForm({ ...registerForm, confirmPassword: e.target.value })
                }
                required
              />
            </div>

            <div className="flex items-center gap-2 mb-6">
              <input
                type="checkbox"
                id="terms"
                className="w-[18px] h-[18px]"
                checked={registerForm.agreeToTerms}
                onChange={(e) =>
                  setRegisterForm({ ...registerForm, agreeToTerms: e.target.checked })
                }
              />
              <label htmlFor="terms" className="text-sm">
                I agree to the{' '}
                <a href="#" className="text-[#0066FF]">
                  Terms of Service
                </a>{' '}
                and{' '}
                <a href="#" className="text-[#0066FF]">
                  Privacy Policy
                </a>
              </label>
            </div>

            {registerError && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-md">
                {registerError}
              </div>
            )}

            <button
              type="submit"
              disabled={registerLoading}
              className="w-full py-3.5 bg-[#0066FF] text-white rounded-lg text-base font-semibold mb-4 hover:bg-[#0052CC] disabled:opacity-50"
            >
              {registerLoading ? 'Creating account...' : 'Create Account'}
            </button>
          </form>

          <div className="flex items-center my-6 text-[#666] text-sm">
            <div className="flex-1 border-b border-[#E5E5E5]"></div>
            <span className="px-4">or sign up with</span>
            <div className="flex-1 border-b border-[#E5E5E5]"></div>
          </div>

          <button className="w-full py-3 bg-white border border-[#D1D1D1] rounded-lg text-[15px] font-medium mb-3 flex items-center justify-center gap-2 hover:bg-[#F5F5F5]">
            <span>🔵</span>
            Sign up with Google
          </button>

          <button className="w-full py-3 bg-white border border-[#D1D1D1] rounded-lg text-[15px] font-medium flex items-center justify-center gap-2 hover:bg-[#F5F5F5]">
            <span>📘</span>
            Sign up with Facebook
          </button>
        </div>
      </div>

      {/* Benefits Section */}
      <div className="max-w-[1200px] mx-auto px-6 pb-12">
        <div className="bg-[#F0F9FF] border border-[#B3E0FF] rounded-xl p-8">
          <h2 className="text-xl font-bold mb-5">Why Create an Account?</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex gap-3">
              <div className="text-2xl flex-shrink-0">🚀</div>
              <div>
                <div className="font-semibold mb-1">Faster Checkout</div>
                <div className="text-sm text-[#666]">
                  Save your shipping and payment information for quick checkout
                </div>
              </div>
            </div>

            <div className="flex gap-3">
              <div className="text-2xl flex-shrink-0">📦</div>
              <div>
                <div className="font-semibold mb-1">Order Tracking</div>
                <div className="text-sm text-[#666]">
                  Track your orders and view your complete purchase history
                </div>
              </div>
            </div>

            <div className="flex gap-3">
              <div className="text-2xl flex-shrink-0">💝</div>
              <div>
                <div className="font-semibold mb-1">Exclusive Offers</div>
                <div className="text-sm text-[#666]">
                  Get access to member-only deals and promotions
                </div>
              </div>
            </div>

            <div className="flex gap-3">
              <div className="text-2xl flex-shrink-0">❤️</div>
              <div>
                <div className="font-semibold mb-1">Wishlist</div>
                <div className="text-sm text-[#666]">
                  Save your favorite products and get notified of price drops
                </div>
              </div>
            </div>

            <div className="flex gap-3">
              <div className="text-2xl flex-shrink-0">🔔</div>
              <div>
                <div className="font-semibold mb-1">Order Updates</div>
                <div className="text-sm text-[#666]">
                  Receive email notifications about your order status
                </div>
              </div>
            </div>

            <div className="flex gap-3">
              <div className="text-2xl flex-shrink-0">💬</div>
              <div>
                <div className="font-semibold mb-1">Easy Support</div>
                <div className="text-sm text-[#666]">
                  Quick access to customer support and order assistance
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
