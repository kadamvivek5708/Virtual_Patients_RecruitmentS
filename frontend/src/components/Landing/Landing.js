import React from 'react';
import { Link } from 'react-router-dom';
import {
  FaHeartbeat, FaBone, FaBrain, FaVial,
  FaShieldAlt, FaLock, FaChartLine, FaRocket
} from 'react-icons/fa';

const FeatureCard = ({ icon: Icon, title, desc }) => (
  <div className="landing-feature">
    <div className="landing-feature-icon"><Icon /></div>
    <h3>{title}</h3>
    <p>{desc}</p>
  </div>
);

const TrialBadge = ({ icon: Icon, label, color }) => (
  <div className={`landing-trial ${color}`}>
    <Icon className="landing-trial-icon" />
    <span>{label}</span>
  </div>
);

const Landing = () => {
  return (
    <div className="landing">
      {/* Top bar */}
      <header className="landing-header">
        <div className="landing-brand">Virtual Patient Recruitment</div>
        <div className="landing-actions">
          <Link to="/login" className="btn ghost">Log In</Link>
          <Link to="/register" className="btn primary">Sign Up</Link>
        </div>
      </header>

      {/* Hero */}
      <section className="landing-hero">
        <div className="landing-hero-inner">
          <div className="landing-hero-title">Connecting Patients to Clinical Trials</div>
          <p className="landing-hero-sub">
            Smarter eligibility, faster enrollment, and a simpler experience for everyone.
          </p>

          {/* Trial badges */}
          <div className="landing-trials">
            <TrialBadge icon={FaHeartbeat} label="Hypertension" color="red" />
            <TrialBadge icon={FaBone} label="Arthritis" color="orange" />
            <TrialBadge icon={FaBrain} label="Migraine" color="purple" />
            <TrialBadge icon={FaVial} label="Phase 1" color="blue" />
          </div>
        </div>

        {/* subtle background */}
        <div className="landing-hero-bg" />
      </section>

      {/* Features */}
      <section className="landing-section">
        <div className="landing-section-title">Why choose our platform?</div>
        <div className="landing-features-grid">
          <FeatureCard icon={FaChartLine} title="Smart Eligibility"
            desc="AI-assisted screening helps match patients to relevant trials quickly." />
          <FeatureCard icon={FaShieldAlt} title="Privacy First"
            desc="We safeguard your information with strong security controls." />
          <FeatureCard icon={FaLock} title="Secure Access"
            desc="Role-based access ensures patients and organizations see what they need." />
          <FeatureCard icon={FaRocket} title="Fast Onboarding"
            desc="Simple steps to apply or upload cohorts and track outcomes in real-time." />
        </div>
      </section>

      {/* How it works (single flow) */}
      <section className="landing-section how">
        <div className="landing-section-title">How it works</div>
        <ol className="landing-steps">
          <li>
            <span className="step-index">1</span>
            <div className="step-content">
              <h4>Create your account</h4>
              <p>Sign up in minutes and access available trials that fit your profile.</p>
            </div>
          </li>
          <li>
            <span className="step-index">2</span>
            <div className="step-content">
              <h4>Apply to a trial</h4>
              <p>Answer a few questions and instantly see if you’re eligible.</p>
            </div>
          </li>
          <li>
            <span className="step-index">3</span>
            <div className="step-content">
              <h4>Track your status</h4>
              <p>View past applications and eligibility outcomes anytime.</p>
            </div>
          </li>
        </ol>
      </section>

      {/* Footer CTA */}
      <section className="landing-footer-cta">
        <div className="footer-cta-box">
          <h3>Ready to get started?</h3>
          <p>Join our platform and accelerate your next step today.</p>
          <div className="landing-cta">
            <Link to="/register" className="btn primary">Get Started</Link>
            <Link to="/login" className="btn ghost">I already have an account</Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Landing;