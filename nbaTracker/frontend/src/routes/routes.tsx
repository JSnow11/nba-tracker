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
} from "components/pages";

export const AppRoutes = () => {
  const isAuthenticated = sessionUtils?.getToken();
  React.useEffect(
    () =>
      console.log(
        `rendered, auth: ${isAuthenticated}`,
        sessionUtils.getToken()
      ),
    [isAuthenticated]
  );

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
          {isAuthenticated ? (
            <>
              <Route path="/team/:abbr" element={<TeamPage />} />
              <Route path="/results" element={<ResultsPage />} />
              <Route path="/standings" element={<StandingsPage />} />
              <Route path="/404" element={<NotFoundPage />} />
              <Route path="*" element={<Navigate to="/404" />} />
            </>
          ) : (
            <Route path="*" element={<LoginPage />} />
          )}
        </Routes>
      </Router>
    </Suspense>
  );
};
