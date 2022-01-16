import React, { Suspense } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";

import { sessionUtils } from "utils";

import { Loader } from "components/01-atoms";
import { Menu } from "components/templates";
import {
  NotFoundPage,
  TeamPage,
  StandingsPage,
  LoginPage,
  ResultsPage,
  RecommendationsPage,
  AdminPage,
} from "components/pages";

export const AppRoutes = () => {
  const token = sessionUtils.getToken();
  const admin = sessionUtils.getAdmin();

  console.log(token, admin);

  const isLoggedIn = !!token && token !== "";
  const isAdmin = !!admin && admin === "true";

  console.log(isLoggedIn, isAdmin);

  return (
    <Suspense
      fallback={
        <div className="h-full w-full flex items-center justify-center">
          <Loader />
        </div>
      }
    >
      <Router>
        <Menu />
        <Routes>
          <Route path="/standings" element={<StandingsPage />} />
          <Route path="/team/:abbr" element={<TeamPage />} />
          <Route
            path="/results/:searchby/:keywords"
            element={<ResultsPage />}
          />
          <Route
            path="/recommendations"
            element={isLoggedIn ? <RecommendationsPage /> : <LoginPage />}
          />
          <Route
            path="/admin"
            element={isLoggedIn && isAdmin ? <AdminPage /> : <LoginPage />}
          />
          <Route path="/404" element={<NotFoundPage />} />
          <Route path="*" element={<Navigate to="/404" />} />
        </Routes>
      </Router>
    </Suspense>
  );
};
